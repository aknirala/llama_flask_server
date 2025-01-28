# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the terms described in the LICENSE file in
# top-level folder for each specific model found within the models/ directory at
# the top-level of this source tree.

# Copyright (c) Meta Platforms, Inc. and affiliates.
# This software may be used and distributed in accordance with the terms of the Llama 3 Community License Agreement.

from flask import Flask, request, jsonify
from io import BytesIO
from pathlib import Path
from typing import Optional
import fire
from llama_models.llama3.api.datatypes import RawMediaItem, RawMessage, RawTextItem
from llama_models.llama3.reference_impl.generation import Llama
import base64

app = Flask(__name__)

THIS_DIR = Path(__file__).parent
generator = None
def run_server(
    ckpt_dir: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 512,
    max_batch_size: int = 4,
    max_gen_len: Optional[int] = None,
    model_parallel_size: Optional[int] = None,
):
    global generator

    print("Loading the model, params:")
    print(f"ckpt_dir: {ckpt_dir}")    
    print(f"max_seq_len: {max_seq_len}")
    print(f"max_batch_size: {max_batch_size}")
    print(f"model_parallel_size: {model_parallel_size}")
    
    print(f"temperature: {temperature}")
    print(f"top_p: {top_p}")

    generator = Llama.build(
        ckpt_dir=ckpt_dir,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
        model_parallel_size=model_parallel_size,
    )

    @app.route('/')
    def home():
        print("Home called")
        dialog = [RawMessage(role="user", content="Are you there?")]
        result = generator.chat_completion(
                dialog,
                max_gen_len=None,
                temperature=0.6,
                top_p=0.9,
            )
        for msg in dialog:
            print(f"{msg.role.capitalize()}: {msg.content}\n")

        out_message = result.generation
        print(f"> {out_message.role.capitalize()}: {out_message.content}")
        print("\n==================================\n")
        response = {
            "role": out_message.role,
            "content": out_message.content,
            "tool_calls": [{"tool_name": t.tool_name, "arguments": t.arguments} for t in out_message.tool_calls]
        }
        return jsonify(response)

    
    @app.route('/generate', methods=['POST'])
    def generate():
        data = request.json
        messages = data.get('messages', [])
        print("Data received: Messages count:", len(messages))

        # Convert received messages into RawMessage objects
        dialog = []
        for msg in messages:
            content = []
            if isinstance(msg['content'], list):  # If content is a list (text + image)
                for item in msg['content']:
                    if item.get('type') == 'text':
                        content.append(RawTextItem(text=item['text']))
                        print(f"Text: {item['text']}")
                    elif item.get('type') == 'image':
                        image_data = base64.b64decode(item['data'])
                        content.append(RawMediaItem(data=BytesIO(image_data)))
                        print(f"Image received (size: {len(item['data'])} bytes in Base64)")
            else:
                content = msg['content']  # Direct text content
                print(f"Text Message: {msg['content']}")
            dialog.append(RawMessage(role=msg['role'], content=content))

        for msg in dialog:
            print("Dialogue received:------------------")
            print(f"{msg.role.capitalize()}: {msg.content}\n")

        result = generator.chat_completion(
        dialog,
        max_gen_len=max_gen_len,
        temperature=temperature,
        top_p=top_p,
        )

        out_message = result.generation
        print("Response:------------------")
        print(f"{out_message.role.capitalize()}: {out_message.content}")

        if hasattr(out_message, "tool_calls"):
            for t in out_message.tool_calls:
                print(f"  Tool call: {t.tool_name} ({t.arguments})")

        response = {
            "role": out_message.role,
            "content": out_message.content,
        }
        return jsonify(response)

    @app.route('/generate1', methods=['POST'])
    def generate1():
        data = request.json
        messages = data.get('messages', [])
        print("data recieved: ", data)
        # Convert received messages to RawMessage objects
        dialog = [RawMessage(role=msg['role'], content=msg['content']) for msg in messages]
        for msg in dialog:
            print("Dialogue recieved:------------------")
            print(f"{msg.role.capitalize()}: {msg.content}\n")

        result = generator.chat_completion(
            dialog,
            max_gen_len=max_gen_len,
            temperature=temperature,
            top_p=top_p,
        )

        out_message = result.generation
        print("Response:------------------")
        print(f"{out_message.role.capitalize()}: {out_message.content}")
        response = {
            "role": out_message.role,
            "content": out_message.content,
        }
        return jsonify(response)

    print("Server is about to start")
    app.run(host='0.0.0.0', port=5000)

def main():
    fire.Fire(run_server)
    



if __name__ == "__main__":
    main()
