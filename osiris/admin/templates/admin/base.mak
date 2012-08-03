<html>
  <head>
    <title>${ title|h }</title>
  </head>
  <body>
    <div class="navbar">
      <div class="navbar-inner">
        <div class="container">
          % if project_url and project_name:
          <a class="brand" href="${ project_url }">${ project_name }</a>
          % endif
          <ul class="nav">
            <li class="active">
              <a href="${ request.route_url(request.route_name, traverse='') }">Home</a>
            </li>
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown">Menu<b class="caret"></b></a>
              <ul class="dropdown-menu">
                % for item in request.admin_menu:
                  <li>
                    <a href="${ request.route_url(request.route_name, traverse=item['name']) }">${ item['title'] }</a>
                  </li>
                % endfor
              </ul>
            </li>
            <li class="divider-vertical"></li>
            <%
               if request.current_user:
                   username = request.current_user.username
               else:
                   username = "guest"
             %>\
            <li><p class="navbar-text">Hello! ${ username|h }</p></li>
          </ul>
          <%
             try:
                 logout_url = request.route_url('logout')
             except KeyError:
                 logout_url = None
           %>
          % if logout_url:
          <ul class="nav pull-right">
            <li><a href="${ logout_url }">Logout</a></li>
          </ul>
          % endif
        </div>
      </div>
    </div>
    <div class="container">
      <h1>${ title|h }</h1>
      ${ next.body() }
    </div>
  </body>
</html>
