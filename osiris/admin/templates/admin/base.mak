<html>
  <head>
    <title>${ title|h }</title>
  </head>
  <body>
    <div class="container-fluid">
      <div class="row-fluid">
        <div class="span2">
          <ul>
          % for item in request.admin_menu:
            <li>
              <a href="${ request.route_url(request.route_name, traverse=item['name']) }">${ item['title'] }</a>
            </li>
          % endfor
          </ul>
        </div>
        <div class="span10">
          <h1>
            <div>${ title|h }</div>
          </h1>
          ${ next.body() }
        </div>
      </div>
    </div>
  </body>
</html>
