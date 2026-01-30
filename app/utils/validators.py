def validate_youtube_url(url: str) -> bool:
    """Valida se é uma URL válida do YouTube"""
    url_str = str(url)
    youtube_domains = ['youtube.com', 'youtu.be', 'www.youtube.com']
    return any(domain in url_str for domain in youtube_domains)
