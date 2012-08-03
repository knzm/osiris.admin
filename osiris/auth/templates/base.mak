<html>
  <head>
    <title>${ title|h }</title>
  </head>
  <body>
    <div class="navbar">
      <div class="navbar-inner">
        <div class="container">
          % if project_url and project_name:
          <a class="brand" href="${ project_url|h }">${ project_name|h }</a>
          % endif
        </div>
      </div>
    </div>
    <div class="container">
      ${ next.body() }
    </div>
  </body>
</html>
