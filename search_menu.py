from web_search import search_web, search_wikipedia


def search_menu():
    print("\n=== Search Menu ===")
    print("1) Web search (DuckDuckGo)")
    print("2) Wikipedia summary")
    print("0) Back\n")

    choice = input("Select an option: ").strip()

    if choice == "1":
        q = input("Enter search query: ")
        result = search_web(q)
        print("\n--- Web Search Result ---")
        print(f"Heading : {result.get('heading')}")
        print(f"Abstract: {result.get('abstract')}")
        print(f"URL     : {result.get('url')}")
    elif choice == "2":
        title = input("Enter Wikipedia title: ")
        result = search_wikipedia(title)
        if not result:
            print("No page found.")
        else:
            print("\n--- Wikipedia Summary ---")
            print(f"Title: {result.get('title')}")
            print(f"URL  : {result.get('url')}")
            print()
            print(result.get("extract"))
    else:
        return

    input("\nPress Enter to continue...")
