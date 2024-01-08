# GSMArena Scraper
## Flow
1. Pull sitemap-phones.xml
2. Filter out any unwanted phone urls
3. Map to a common data structure
```json
{
    "id": "string",
    "make": "string",
    "model": "string",
    "url": "string"
}
```
4. For each phone in sitemap, issue a randomly timed GET request to `.url` and pull page HTML
5. Map `div#spec-table` HTML to a common data structure, extending the above
```json
{
    "id": "string",
    "make": "string",
    "model": "string",
    "url": "string",
    "specs": "list[dict[string,string]]"
}
```
6. Every block of 50, dump the found and failed devices to files and wait for 10 secs

