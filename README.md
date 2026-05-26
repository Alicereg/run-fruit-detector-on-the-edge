# Fruit Detector Edge AI

Exported from Azure Custom Vision.

## Install Requirements

```bash
pip install -r requirements.txt
```

---

## Install Docker Desktop

Download Docker Desktop:

https://www.docker.com/products/docker-desktop

Make sure Docker Desktop is running before continuing.

Verify installation:

```bash
docker --version
```

---

## Build Docker Container

```bash
docker build -t classifier:v2 .
```

---

## Run Docker Container

```bash
docker run -p 127.0.0.1:80:80 -d classifier:v2
```

Local API endpoint:

```text
http://127.0.0.1/image
```

---

## Run the Application

Open another terminal:

```bash
python demo.py
```

---

## Application Modes

### Webcam Mode
- Press `S` to scan fruit
- Press `Q` to quit

### Image File Mode
- Select image from File Explorer
- AI predicts fruit freshness

---

## API Examples

### multipart/form-data

```bash
curl -X POST http://127.0.0.1/image -F imageData=@test.jpg
```

### application/octet-stream

```bash
curl -X POST http://127.0.0.1/image -H "Content-Type: application/octet-stream" --data-binary @test.jpg
```

---

## Example Output

```text
Ripe Orange: 99.84% | Edge: 0.11s
```
