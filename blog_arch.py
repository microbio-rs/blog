#!/usr/bin/env python3
#
# Copyright (c) 2023 Murilo Ijanc' <mbsd@m0x.ru>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.general import Client, User
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import CF, CloudFrontEdgeLocation, Route53
from diagrams.aws.security import ACM
from diagrams.aws.storage import S3

# output filename, default extension is png
filename = "arch"


def create_diagram():
    with Diagram("blog architecture - microbio.rs", show=False, filename=filename):
        user = User("User")
        with Cluster("AWS Cloud"):
            # lambda_edge = CloudFrontEdgeLocation("Security response\nheaders")
            route = Route53("DNS microbio.rs")
            s3 = S3("blog.microbio.rs")
            with Cluster("Front") as front:
                cf = CF("CloudFront")
                acm = ACM("Cert *.microbio.rs")
                cf - acm 
            user >> route >> Edge(label="cached?") >> cf
            cf >> Edge(label="obtem arquivo") >> s3
            user << route << cf
            # cf << lambda_edge


if __name__ == "__main__":
    create_diagram()
