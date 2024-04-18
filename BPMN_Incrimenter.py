import re


class BPMN_Incrimenter:
    def __init__(self, user_input: re.Match) -> None:
        self.first_number: str = user_input.group(2)
        self.second_number: str = user_input.group(3)
        self.last_number: str = user_input.group(4)

    def __choose_pattern(self) -> str:
        if self.last_number:
            return (
                r"name=\"("
                + self.first_number
                + r"\."
                + self.second_number
                + r"\.?(\d{1,2})?)"
            )
        elif self.second_number:
            return r"name=\"(" + self.first_number + r"\.?(\d{1,2})?)"
        else:
            return r"name=\"((" + self.first_number + r")\.)"

    def __choose_replacment_str(self, match: re.Match) -> str:
        if self.last_number:
            return f'name="{self.first_number}.{self.second_number}.{int(match.group(2)) + 1}'
        elif self.second_number:
            return f'name="{self.first_number}.{int(match.group(2)) + 1}'
        else:
            return f'name="{int(match.group(2)) + 1}.'

    def __retry_or_continue(self, match: re.Match) -> bool:
        if self.last_number and int(self.last_number) > int(match.group(2)):
            return True
        elif (
            not self.last_number
            and self.second_number
            and int(self.second_number) > int(match.group(2))
        ):
            return True
        elif (
            not self.last_number
            and not self.second_number
            and int(self.first_number) < int(match.group(2))
        ):
            return True

        return False

    def incriment_strings(self, string_list: list[str]) -> None:
        # Full string => 4.1.2
        # 0-> 4.1.2 | 1-> 4.1.2 | 2-> 4 | 3-> 1 | 4-> 2
        pattern: str = self.__choose_pattern()

        for i in range(len(string_list)):
            match: re.Match | None = re.search(pattern, string_list[i])
            if match is None:
                continue
            if self.__retry_or_continue(match):
                continue

            replacment_str: str = self.__choose_replacment_str(match)

            string_list[i] = string_list[i].replace(
                f'name="{match.group(1)}',
                replacment_str,
            )

    def increment_range(self, string_list: list[str]) -> None:
        raise NotImplementedError()
