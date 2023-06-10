---
title: Primeiro post
published_date: 2023-06-08 21:31:10 +0000
layout: blog.liquid
is_draft: false
description: arquitetura inicial do blog
---
# Primeiro post
<p><img src="/static/img/arch.png" width="900px"></p>

Nada como no primeiro post para comentar um pouco sobre a arquitetura do blog
utilizando os recursos da aws. Caso queira conferir o código você consegue 
ver [aqui][0].

Por enquanto um único repositório centraliza a infra estrutura das
aplicações, essa é uma decisão inicial que provavelmente será alterada no
futuro, por enquanto essa centralização irá facilitar alguns processos. 

Para o IaC estou utilizando módulos do [terraform][1] e [terragrunt][2] que
utiliza desses módulos para construir de ponta-a-ponta a estrutura da aplicação.
A decisão do [terragrunt][2] foi mais pensando nos seguintes fatores:

```
.
├── terraform
│   ├── modules               <-- módulos utilizados pelo terragrunt
│   │   ├── github-repo
│   │   ├── network
│   │   │   ├── dns
│   │   │   └── dns-record
│   │   ├── static-website
│   │   └── storage
└── terragrunt
    ├── applications
    │   └── prod
    │       └── blog
    └── shared                <-- compartilhados com as aplicações
        └── prod
            └── network
                └── dns
```

1. Facilidade gerir o estado em diversos ambientes
2. Reutilização de código
3. Bem mais legível
4. Facilidade em administrar as configurações.

Como podem perceber pelo código assumi alguns pontos:

```tf
inputs = {
  static_website = {
    dns = {
      zone_id = dependency.dns.outputs.zone_id
    }

    description = "microbio.rs blog"
    error_page = "error.html"
    index_page = "index.html"
    name = "blog"
  }
}
```

1. Todo e qualquer projeto futuro será criado um repositório.
2. Todo repositório terá a branch **trunk** protegida.
3. Repositórios de projeto não possuem wiki.
4. Recursos que são compartilhados ficam na pasta **shared**. Exemplos:
   Route53, CloudFront, Vpc, subnets...

Futuramente posso ir adicionando outras opções por exemplo restrição de times,
usuários, secrets aos repositórios...

Além dos padrões para repositório acima foi criado um módulo para [site
estático][4] o qual cria a arquitetura da imagem acima, ainda faltam alguns
pontos de segurança que ficará como *ToDo* para o próximo post.

- [x] Dnssec
- [x] Log do cloudfront (iremos centralizar isso em um bucket de logs)
- [ ] WAF (Algumas acl básicas)
- [ ] Shield 
- [ ] Cabeçalhos de segurança na resposta do cloudfront

[0]: https://github.com/microbio-rs/mb-platform/blob/master/terragrunt/applications/prod/blog/terragrunt.hcl
[1]: https://www.terraform.io/
[2]: https://terragrunt.gruntwork.io/
[4]: https://github.com/microbio-rs/mb-platform/blob/master/terraform/modules/static-website/main.tf
