import string
import re
import requests

files = {
    "Alice's Adventures in Wonderland": "alice.txt",
    "The War of the Worlds": "war_of_the_worlds.txt",
    "The Adventures of Sherlock Holmes": "sherlock_holmes.txt",
    "The Picture of Dorian Gray": "dorian_gray.txt",
    "Winnie-the-Pooh": "winnie_the_pooh.txt"
}


def fetch_text(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        raise ValueError(f"File {filename} not found.")


def save_text(title, text):
    filename = f"{title}.txt"
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(text)
    print(f"Saved {title} as {filename}")


def process_file(fname):
    with open(fname, 'r', encoding='utf-8') as file:
        dat = file.read()
        dat = re.sub(r'\*\*\*.*?\*\*\*', '', dat, flags=re.DOTALL)
    return re.findall(r'\b\w+\b', dat.lower())


def words_to_dict(words):
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    return word_count


def get_statistics(words):
    total_words = len(words)
    unique_words = len(set(words))
    return total_words, unique_words


def calculate_ttr(total_words, unique_words):
    return unique_words / total_words if total_words > 0 else 0


def main():
    titles = list(files.keys())

    for title in titles:
        try:
            text = fetch_text(files[title])
            save_text(title, text)
        except ValueError as e:
            print(f"Error fetching text for {title}: {e}")
            continue

    while True:
        print("\nSelect two texts for comparison:")
        for i, title in enumerate(titles, start=1):
            print(f"{i}. {title}")

        try:
            choice1 = int(input("Enter the number of the first text: ")) - 1
            choice2 = int(input("Enter the number of the second text: ")) - 1
            if choice1 not in range(len(titles)) or choice2 not in range(len(titles)):
                raise ValueError("Invalid choice.")
        except ValueError as e:
            print(f"Invalid input: {e}")
            continue

        try:
            text1 = process_file(files[titles[choice1]])
            text2 = process_file(files[titles[choice2]])
        except FileNotFoundError as e:
            print(f"Error: {e}")
            continue

        total_words1, unique_words1 = get_statistics(text1)
        total_words2, unique_words2 = get_statistics(text2)

        print(f"\nStatistics for {titles[choice1]}:")
        print(f"Total words: {total_words1}")
        print(f"Unique words: {unique_words1}")

        print(f"\nStatistics for {titles[choice2]}:")
        print(f"Total words: {total_words2}")
        print(f"Unique words: {unique_words2}")

        ttr1 = calculate_ttr(total_words1, unique_words1)
        ttr2 = calculate_ttr(total_words2, unique_words2)

        print(f"TTR for {titles[choice1]}: {ttr1:.4f}")
        print(f"TTR for {titles[choice2]}: {ttr2:.4f}")

        if abs(total_words1 - total_words2) > 3000:
            print("TTR is not a reliable comparison for chosen texts.")
        else:
            print("TTR is between comparable texts.")

        search_word = input("Enter a word to search for: ").lower()
        count1 = text1.count(search_word)
        count2 = text2.count(search_word)

        print(f"'{search_word}' appears {count1} times in {titles[choice1]}.")
        print(f"'{search_word}' appears {count2} times in {titles[choice2]}.")

        if input("Do you want to compare two new texts? (yes/no): ").strip().lower() != 'yes':
            break


if __name__ == "__main__":
    main()
