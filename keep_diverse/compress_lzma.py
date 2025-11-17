def compress_lzma(btext: bytes) -> int:
    import lzma

    return len(lzma.compress(btext))
