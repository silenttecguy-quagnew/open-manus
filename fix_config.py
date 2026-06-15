import io, os, re;
f=io.open("app/config.py", "r", encoding="utf-8");
c=f.read();
f.close();
# Find the DaytonaSettings class and the daytona_api_key field
# Change it to be optional with a None default to satisfy Pydantic
c = c.replace("daytona_api_key: str", "daytona_api_key: Optional[str] = None")
f=io.open("app/config.py", "w", encoding="utf-8");
f.write(c);
f.close()
