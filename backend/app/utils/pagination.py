def normalize_page(page: int, page_size: int) -> tuple[int, int]:
    normalized_page = page if page > 0 else 1
    normalized_page_size = page_size if 0 < page_size <= 50 else 20
    return normalized_page, normalized_page_size
