def is_valid(title):
    if not title:
        return False

    bad_words = ["ad", "sponsored", "promo", "advertisement"]
    good_words = ["nike", "adidas", "shoe", "sneaker"]  

    t = title.lower()

    for word in bad_words:
        if word in t:
            return False

    if good_words:
        return any(word in t for word in good_words)

    return True
