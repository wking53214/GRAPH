# --- Execution Driver ---
async def run_demo():
   # 1. Define the module
   uim = UserInputModule()
   adapter = GsaUniversalAdapter(uim, "v1.1")
   
   # 2. Setup the initial envelope (the state carrier)
   envelope = ContextEnvelope(
       header_mapping=MappingProxyType({"gsa_loop_iteration": 0}),
       user_input_payload={"user_data": "Hello World"},
       ai_output_payload={},
       combined_optimized_payload={}
   )
   
   # 3. Process
   result_envelope, payload = await adapter.process_payload(envelope)
   
   # 4. Show the output
   print(f"Status: {result_envelope.status_string}")
   print(f"Payload: {payload}")

if __name__ == "__main__":
   asyncio.run(run_demo())