import re
import subprocess


def run_dig(domain, target_server=None, time=5, tries=1, stats=True, norecurse=False):
    """
    Execute a dig command
    :param domain: the domain to run a DNS query on
    :param target_server: (optional) the recursive server to make the request to
    :param time: the +time parameter to dig (timeout). Default: 5
    :param tries: the +tries parameter to dig (number of retries after failure). Default: 1
    :param stats: whether to display stats (+stats). Default: True
    :param norecurse: whether to disable recursion (+norecurse). Default: False
    :return: DigResults with parsed results if successful, None otherwise.
    """

    args = ["dig"]

    # Only include "@" field if target server is provided
    if target_server is not None:
        args.append("@{}".format(target_server))
    args.append(domain)
    args.append("+time={}".format(time))
    args.append("+tries={}".format(tries))
    if stats:
        args.append("+stats")
    if norecurse:
        args.append("+norecurse")

    # Run and decode
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
    stdout, _ = process.communicate(None)
    raw = stdout

    output = raw.decode('utf-8')

    try:
        return DigResults.parse(output)
    except AttributeError:
        raise Exception('AttributeError', output)


class DigResults:
    def __init__(self, answer, authority, additional, status, responding_server,
                 answer_section, authority_section, additional_section, query_time,
                 msg_size, recursion_not_available):
        """

        :param answer: integer: number of answer section responses
        :param authority: integer: number of authority section responses
        :param additional: integer: number of additional section responses
        :param status: the status field of the response. Usually 'NOERROR' or 'NXDOMAIN'
        :param responding_server: the responding server's IP address
        :param answer_section: an array of DigSectionLine objects corresponding to the number of responses
        :param authority_section: an array of DigSectionLine objects corresponding to the number of responses
        :param additional_section: an array of DigSectionLine objects corresponding to the number of responses
        :param query_time: Query time field
        :param msg_size: the MSG SIZE field
        :param recursion_not_available: whether the phrase "recursion requested but not available" appeared
        """

        self.recursion_not_available = recursion_not_available
        self.msg_size = msg_size
        self.query_time = query_time
        self.ANSWER = answer
        self.AUTHORITY = authority
        self.ADDITIONAL = additional
        self.status = status
        self.responding_server = responding_server
        self.additional_section = additional_section
        self.authority_section = authority_section
        self.answer_section = answer_section

    @staticmethod
    def parse(output):
        """
        Parse dig output and return a DigResults object if possible
        :param output: dig output
        :return: DigResults or None
        """
        lines = output.split("\n")

        output = output.replace("\n", " ")

        successful = ";; connection timed out" not in output
        if len(output) == 0 or not successful:  # Connection timed out, no point in continuing
            return None

        status = re.match(r'.*status: ([A-Z]+),.*', output).group(1)
        authority_count = int(re.match(r'.*AUTHORITY: (\d+),.*', output).group(1))
        answer_count = int(re.match(r'.*ANSWER: (\d+),.*', output).group(1))
        additional_count = int(re.match(r'.*ADDITIONAL: (\d+).*', output).group(1))
        responding_server = re.match(r'.*;; SERVER: (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*', output).group(1)
        query_time = int(re.match(r'.*Query time: (\d+) msec.*', output).group(1))
        msg_size = int(re.match(r'.*MSG SIZE +rcvd: (\d+).*', output).group(1))
        recursion_not_available = "recursion requested but not available" in output

        authority_section = []
        additional_section = []
        answer_section = []

        in_ans = False
        in_auth = False
        in_add = False

        for line in lines:
            # Update the section we're in
            if "ANSWER SECTION" in line:
                in_ans = True
                in_auth = False
                in_add = False
                continue
            if "AUTHORITY SECTION" in line:
                in_ans = False
                in_auth = True
                in_add = False
                continue
            if "ADDITIONAL SECTION" in line:
                in_ans = False
                in_auth = False
                in_add = True
                continue

            # Only attempt to parse a line if we're in an answer section
            if in_ans or in_auth or in_add:
                # Attempt to parse the line
                line_parsed = DigSectionLine.parse(line)

                # If successful, add the line result to the appropriate list
                if line_parsed is not None:
                    if in_ans:
                        answer_section.append(line_parsed)
                    if in_auth:
                        authority_section.append(line_parsed)
                    if in_add:
                        additional_section.append(line_parsed)

        return DigResults(status=status, answer=answer_count, authority=authority_count, additional=additional_count,
                          responding_server=responding_server, query_time=query_time, msg_size=msg_size,
                          authority_section=authority_section, answer_section=answer_section,
                          additional_section=additional_section, recursion_not_available=recursion_not_available)

    def __str__(self):
        return "status: {}, query time: {}, message size: {}, responding server: {}, " \
               "ANSWER: {}, AUTHORITY: {}, ADDITIONAL: {}" \
               "\n\tANSWER section: {}" \
               "\n\tAUTHORITY section: {}" \
               "\n\tADDITIONAL section: {}".format(self.status, self.query_time, self.msg_size, self.responding_server,
                                                   self.ANSWER, self.AUTHORITY, self.ADDITIONAL,
                                                   [str(l) for l in self.answer_section],
                                                   [str(l) for l in self.authority_section],
                                                   [str(l) for l in self.additional_section])


class DigSectionLine:
    def __init__(self, name, ttl, response_class, record_type, ip):
        self.ip = ip
        self.record_type = record_type
        self.response_class = response_class
        self.ttl = ttl
        self.name = name

    @staticmethod
    def parse(line):
        result = re.search(r'^(\S+)\s+(\d+)\s+([A-Z]+)\s+([A-Z]+)\s+(.*)', line)
        if result is not None:
            return DigSectionLine(result.group(1),
                                  int(result.group(2)),
                                  result.group(3),
                                  result.group(4),
                                  result.group(5))
        else:
            return None

    def __str__(self):
        return "[name: {}, ttl: {}, class={}, type={}, ip={}]".format(self.name,
                                                                      self.ttl,
                                                                      self.response_class,
                                                                      self.record_type,
                                                                      self.ip)
