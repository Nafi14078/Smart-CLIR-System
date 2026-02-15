def overlap(system_results, google_results):
    system_urls = set([r["url"] for r in system_results])
    google_urls = set(google_results)

    intersection = system_urls.intersection(google_urls)

    return {
        "Overlap Count": len(intersection),
        "Overlap %": round(len(intersection) / len(google_urls), 2)
    }
