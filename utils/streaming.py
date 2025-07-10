from context import UserSessionContext

async def stream_response(agent, input_text: str, context: UserSessionContext):
    result = await agent.process_input(input_text, context)

    if result.get("status") == "success" and "message" in result:
        print("\n💡 Advice:\n" + result["message"] + "\n")
    elif "message" in result:
        print("\n📢 " + result["message"] + "\n")
    elif "error" in result:
        print("❌ Error:", result["error"])
        if "details" in result:
            print("Details:", result["details"])
    else:
        print("❓ I didn’t understand. Please rephrase.")
