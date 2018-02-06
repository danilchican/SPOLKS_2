from ip.ipv4 import AUTO_VALUE

CARRY_AND = 0xFFFF
CARRY_SHIFT = 16
DATA_SHIFT = 8


class Helper:
    @staticmethod
    def find_checksum(data):
        answer = AUTO_VALUE
        for i in range(AUTO_VALUE, len(data), 2):
            temp = data[i] + (data[i + 1] << DATA_SHIFT)
            answer = Helper.carry_around_sum(answer, temp)
        return ~answer & CARRY_AND

    @staticmethod
    def carry_around_sum(first, second):
        carry = first + second
        return (carry & CARRY_AND) + (carry >> CARRY_SHIFT)
