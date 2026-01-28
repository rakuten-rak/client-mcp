async def run_chat(handler) -> None:
    """Run an Ai Powered Handler Chat Session"""
    print("\n MCP Client's Chat Session")
    print("\n Type your queries or 'quit' to exist.")
    while True:
        try:
            if not (query := input("\nYou:: ").strip()):
                continue
            if query.lower == "quit":
                break
            print("\n" + await handler.process_query(query))
             
        except Exception as e:
            print(f"\Error : {str(e)}")
            
    print("\n Goodbye!!!")