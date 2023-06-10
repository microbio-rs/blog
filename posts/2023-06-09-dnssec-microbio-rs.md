---
title: dnssec microbio.rs
description: adicionado dnssec no route53
published_date: 2023-06-09 18:33:19 +0000
layout: blog.liquid
is_draft: false
---
# DNSSEC no route53

Continuando do [último post][0] havia ficado um ToDo para melhorarmos
não somente a arquitetura do blog mas como algumas questões de segurança. Via
[terraform][1] criei uma chave com o kms e apliquei ao [route53][2] para termos
suporte a [DNSSEC][5].

O código pode ser visto [aqui][3].

## Conferindo assinatura

Existem várias ferramentas online para checar se a zona está assinando as
requisições eu utilizo o programa *dig*. 

```console
dig microbio.rs dnskey +dnssec
```

Um retorno como abaixo deve ser visto:

```
; <<>> dig 9.10.8-P1 <<>> microbio.rs dnskey +dnssec
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 39804
;; flags: qr rd ra; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags: do; udp: 1232
;; QUESTION SECTION:
;microbio.rs.                   IN      DNSKEY

;; ANSWER SECTION:
microbio.rs.            3504    IN      DNSKEY  257 3 13 sX38AB0sM0Qw8tsM/pIOdjYicR87748HSRabEG2+I/AVNMoSazaLhiN7 tSc3nIjAddU6VElmYZ6QnwsVPLtzgw==
microbio.rs.            3504    IN      DNSKEY  256 3 13 gMGo0IGYtuhDM3YY8nYFJGVutn+GoCH9/WxRr88XKMDPB48BrwOaGnkH TmSamP3tGlbe8C2dlMaEPwnnaA3WMg==
microbio.rs.            3504    IN      RRSIG   DNSKEY 13 2 3600 20230611020000 20230610150000 6456 microbio.rs. pvqB1QtkAG2cfSBe4D9hHBXQ8mmkiv4J5WFBfVuFphYwkl0HcZY6o2Bj mxOYAHRh6IHnMG4szRwgd3po5wsB/w==

;; Query time: 0 msec
;; SERVER: 46.23.91.20#53(46.23.91.20)
;; WHEN: Sat Jun 10 15:50:21 -03 2023
;; MSG SIZE  rcvd: 307

```

Caso não apareça, aguarde um pouco por causa do cache do seu dns, no meu caso
enquanto estava em cache uma saída como essa era vista:

```
; <<>> DiG 9.18.15 <<>> microbio.rs dnskey +dnssec
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOTIMP, id: 2500
;; flags: qr rd ad; QUERY: 1, ANSWER: 0, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags: do; udp: 1232
; COOKIE: 6155db0c4d6ccb13 (echoed)
;; QUESTION SECTION:
;microbio.rs.                   IN      DNSKEY

;; Query time: 3 msec
;; SERVER: 127.0.0.1#53(127.0.0.1) (UDP)
;; WHEN: Sat Jun 10 15:55:21 -03 2023
;; MSG SIZE  rcvd: 52

```

### Alterando na registradora

No entanto não adianta somente fazer as configurações acima, isso porque
a registradora tem que adicionar as informações geradas pelo [route53][2] na
configuração do seu domínio. Algumas registradoras permitem fazer isso via
painel no meu caso para o domínio .rs utilizo a registradora [Istanco][6]
e tive que entrar em contato via suporte para eles adicionarem as
configurações.

Geralmente as informações que as registradoras necessitam:

- Key tag (KSK key ID)
- Algorithm
- Digest type
- Digest

> Todas as inforações acima podem ser vista no [route53][2].


Após confirmado pela registradora a operação é possível confirmar:

1. Obtemos as autoridades principais, para isso digite o comando abaixo:
```console
dig rs NS +short
```

Uma saída como abaixo deve aparecer, óbvio substitua o `rs` pelo sufixo do seu domínio.

```
f.nic.rs.
g.nic.rs.
b.nic.rs.
a.nic.rs.
l.nic.rs.
h.nic.rs.
```

Agora checamos a entrada `DS` utilizando @ para indicar com servidor de dns quero utilizar.

```console
dig microbio.rs DS @a.nic.rs
```

A saída abaixo mostra na seção de resposta o registro `DS`:

```
; <<>> dig 9.10.8-P1 <<>> microbio.rs DS @a.nic.rs
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 19969
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;microbio.rs.                   IN      DS

;; ANSWER SECTION:
microbio.rs.            3600    IN      DS      6456 13 2 26C662EA8108E5B6556F62129EBB14302D2FD0500FB7973B6827652D 44232A2C

;; Query time: 31 msec
;; SERVER: 91.199.17.59#53(91.199.17.59)
;; WHEN: Sat Jun 10 19:55:25 -03 2023
;; MSG SIZE  rcvd: 88
```

### Testando

```
```

## Porque DNSSEC?

[DNSSEC][5] para quem não sabe é a sigla para (Domain Name System Security
Extensions) isso ajuda a manter uma "internet" mais segura.

A implementação do [DNSSEC][5] ajuda a mitigar esses riscos de segurança,
fornecendo autenticação e integridade dos registros DNS. Ele utiliza
criptografia de chave pública para assinar digitalmente os registros DNS,
garantindo que eles não tenham sido alterados ou corrompidos durante
o trânsito.

Alguns dos principais motivos pelos quais o [DNSSEC][5] é importante:

1. Autenticação dos registros DNS
2. Integridade dos dados
3. Prevenção de ataques de envenenamento de cache
4. Proteção contra ataques de sequestro de DNS
5. Confiança nas transações online

Em resumo, o [DNSSEC][5] desempenha um papel crucial na melhoria da segurança do
DNS, protegendo os usuários contra ataques de redirecionamento e falsificação
de dados. Sua implementação ajuda a fortalecer a infraestrutura da Internet
e a garantir uma experiência mais segura e confiável para os usuários finais.


[0]: www.google.com
[1]: https://www.terraform.io/
[2]: https://aws.amazon.com/pt/route53/
[3]: https://github.com/microbio-rs/mb-platform/blob/aee12a4650b31e0137240b02d0b58217ca79d04e/terraform/modules/network/dns/main.tf#L50
[5]: https://pt.wikipedia.org/wiki/DNSSEC
[6]: https://www.istanco.rs/
[7]: https://dnssec-analyzer.verisignlabs.com/
