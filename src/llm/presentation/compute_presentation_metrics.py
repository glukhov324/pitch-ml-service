


def compute_ppt_metrics(slides_data):
    total_words = sum(s["word_count"] for s in slides_data)
    total_imgs = sum(s["img_count"] for s in slides_data)
    return {
        "slides": len(slides_data),
        "total_words": total_words,
        "total_images": total_imgs,
        "avg_words_per_slide": total_words / len(slides_data),
        "slides_with_images": sum(1 for s in slides_data if s["img_count"] > 0),
    }