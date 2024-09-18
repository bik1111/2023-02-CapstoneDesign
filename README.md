# 2023-02-CapstoneDesign

## 1. Research Title
채팅 서비스 구현 시 효율적인 라이브러리 선택을 위한 gRPC 및 zeroMQ 성능 비교 및 분석 <br>

## 2. Research Object

채팅 서비스를 도입하려는 기업 및 서비스에게 효율적인 라이브러리 선택을 위한 인사이트 제공 <br>

## 3. Research Model

- Independent Variable: <b>zeroMQ, gRPC</b> <br>
- Controlled Variable: <b>Message Transmission Count, Message Size</b>
- Dependent Variable: <b>Transmission Speed, Throughput(message/s), CPU Usage </b>

## 4. Research Method

- gRPC: <b>Implementing asynchronous programming using Python Module Asyncio. </b>
- zeroMQ: <b>Implementing a bidirectional streaming with PUB/SUB + PUSH/PULL patterns. </b>

## 5. Research Results


### 5-1. Transmission Speed Aspect

<img width="840" alt="image" src="https://github.com/bik1111/2023-02-CapstoneDesign/assets/76617139/2d4e2dbe-8890-45ea-958e-1ca67a4627f5">

---
### 5-2. CPU Usage Aspect
<img width="840" alt="image" src="https://github.com/bik1111/2023-02-CapstoneDesign/assets/76617139/3a12822c-0aea-4a9a-94cd-86d51aea4410">


---

### 5-3. Measuring the elapsed time and throughput (messages per second) when sending messages of a specific byte size.
<img width="500" alt="image" src="https://github.com/bik1111/2023-02-CapstoneDesign/assets/76617139/a25c1c1f-6b4a-4ad8-9bfe-8a66be407ed8">
<img width="500" alt="image" src="https://github.com/bik1111/2023-02-CapstoneDesign/assets/76617139/923f4833-f9e8-4159-96da-9cea5e598b66">

---

## 6. Reference

- https://scholar.google.com/scholar?hl=ko&as_sdt=0%2C5&q=exploring+the+impact+of+chatbots+on+consumer+sentiment&btnG=
- https://scholar.google.com/scholar?hl=ko&as_sdt=0%2C5&q=STUDYING+SYSTEMS+OF+OPEN+SOURCE+MESSAGING&btnG=
- https://fdik.org/wikileaks/year0/vault7/cms/files/The%20Architecture%20of%20Open%20Source%20Applications%20(Volume%202)_%20ZeroMQ.pdf
- https://www.igvita.com/2010/09/03/zeromq-modern-fast-networking-stack/
- https://www.sedaily.com/NewsView/29OFG5G6XW
- https://www.techm.kr/news/articleView.html?idxno=106416
- https://books.google.co.kr/books?hl=ko&lr=&id=883LDwAAQBAJ&oi=fnd&pg=PR2&dq=gRPC&ots=jvoTaR9CAA&sig=fiQ8s6FGY5BYr28bKWSVB_n0r5I&redir_esc=y#v=onepage&q=gRPC&f=false
- https://web.archive.org/web/20220508010157id_/https://dl.acm.org/doi/pdf/10.1145/3476883.3520220
- https://www.vinsguru.com/grpc-server-streaming/
- https://learning-0mq-with-pyzmq.readthedocs.io/en/latest/pyzmq/patterns/pubsub.html#

 ---
 

### 7. Material

- https://docs.google.com/presentation/d/16x8lrbJkRjA1yNrHj7mozVZD4qMdgBiD/edit?usp=sharing&ouid=117021856449870949642&rtpof=true&sd=true
















 

