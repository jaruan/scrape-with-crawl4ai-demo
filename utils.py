def match_str(target_str: str, matched_strs: list[str]) -> bool:
    for str in matched_strs:
        if str in target_str:
            return True

    return False
