""" miscelaneous util functions """

import io


def is_raspberry_pi(raise_on_errors: bool = False) -> bool:
    """Checks if Raspberry PI.
    :return:
    """
    try:
        with io.open("/proc/cpuinfo", "r", encoding="utf-8") as cpuinfo:
            found = False
            for line in cpuinfo:
                if line.startswith("Hardware"):
                    found = True
                    _, value = line.strip().split(":", 1)
                    value = value.strip()
                    if value not in (
                        "BCM2708",
                        "BCM2709",
                        "BCM2711",
                        "BCM2835",
                        "BCM2836",
                    ):
                        if raise_on_errors:
                            raise ValueError("This system does not appear to be a Raspberry Pi.")
                        return False
            if not found:
                if raise_on_errors:
                    raise ValueError(
                        "Unable to determine if this system is a Raspberry Pi."
                    )
                return False
    except IOError as ex:
        if raise_on_errors:
            raise ValueError("Unable to open `/proc/cpuinfo`.") from ex
        return False

    return True
