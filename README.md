## Flask Best Web Framework Blueprint File Structure [STATE OF THE ART FRAMEWORK FOR WEB DEVELOPMENT]

## For auto reloading

<p>
105

Ultimately this is a frustrating browser cache issue, which can be solved by forcing the browser to do a "hard refresh", which is going to be a browser/OS dependent keystroke, but generally this works:

```bash
Windows: Ctrl+F5
Mac: Cmd+Shift+R
Linux: Ctrl+Shift+R

```

There are other filename tricks one can use to avoid this issue (mentioned in comments of the OP). These are especially important in production where you have no control over browser behavior.

For non-Static Flask responses you can set the cache_control.max_age property, which should tell the browser when to expire the response if it is cached. For instance if you have a Flask XHR endpoint that returns JSON data you could do this:

</p>

https://stackoverflow.com/questions/41144565/flask-does-not-see-change-in-js-file
#Facial-Recognition-App
