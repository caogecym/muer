def find_between(s, start, end, inclusive=False):
    try:
        start_idx = s.index(start) + len(start) 
        end_idx = s.index(end, start_idx)

        if inclusive:
            return s[start_idx-len(start):end_idx+len(end)]
        else:
            return s[start_idx:end_idx]

    except ValueError:
        return ""
