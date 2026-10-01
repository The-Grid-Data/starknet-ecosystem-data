"""Fetch a snapshot of every Starknet-tagged profile from The Grid's public GraphQL API.

Usage: python3 scripts/fetch_snapshot.py starknetdata-<month>-<year>.json

Writes {"data": {"roots": [...]}} ordered by root id, so successive snapshots
diff cleanly. Reads anonymously -- no credentials needed.
"""

import json
import ssl
import sys
import urllib.request

ENDPOINT = "https://beta.node.thegrid.id/graphql"
TAG_ID = "id1738748042-W5oej0O8QJezGZ0RPXAHFg"  # the "Starknet" external profile tag
PAGE_SIZE = 50

QUERY = """
query Starknet($tag: String!, $limit: Int!, $offset: Int!) {
  roots(
    where: {profileTags: {tagId: {_eq: $tag}}}
    limit: $limit
    offset: $offset
    order_by: {id: Asc}
  ) {
    id
    slug
    profileInfos {
      id
      name
      tagLine
      descriptionShort
      descriptionLong
      foundingDate
      iconMedia: media(where: {mediaType: {name: {_eq: "Icon"}}}) { url mediaType { name } }
      logoMedia: media(where: {mediaType: {name: {_eq: "Logo on white"}}}) { url mediaType { name } }
      profileSector { id name definition }
      profileStatus { id name definition }
      profileType { id name definition }
      urls { url urlType { name } }
    }
    socials { id name socialType { id name definition } urls { url } }
    products {
      id
      name
      description
      isMainProduct
      launchDate
      productStatus { id name definition }
      productType { id name definition }
      urls { url urlType { name } }
    }
    assets {
      id
      name
      ticker
      description
      assetStatus { id name definition }
      assetType { id name definition }
      urls { url urlType { name } }
    }
  }
}
"""

def ssl_context():
    # Python installed from python.org ships no root certificates on macOS; fall
    # back to certifi when the system store is empty.
    try:
        import certifi
    except ImportError:
        return ssl.create_default_context()
    return ssl.create_default_context(cafile=certifi.where())


SSL_CONTEXT = ssl_context()


def gql(variables):
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Content-Type": "application/json"},
    )
    body = json.loads(
        urllib.request.urlopen(request, timeout=120, context=SSL_CONTEXT).read()
    )
    if body.get("errors"):
        sys.exit(json.dumps(body["errors"], indent=2))
    return body["data"]["roots"]


def main(destination):
    roots, offset = [], 0
    while True:
        page = gql({"tag": TAG_ID, "limit": PAGE_SIZE, "offset": offset})
        roots.extend(page)
        if len(page) < PAGE_SIZE:
            break
        offset += PAGE_SIZE

    with open(destination, "w", encoding="utf-8") as handle:
        json.dump({"data": {"roots": roots}}, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(f"wrote {len(roots)} profiles to {destination}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
