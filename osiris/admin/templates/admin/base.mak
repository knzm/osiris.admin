<html>
  <head>
    <title>${ request.model_name or 'root'|h }</title>
    <link rel="stylesheet" href="${ request.static_url('pyramid_formalchemy:static/admin.css')|h }"></link>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js"></script>
  </head>
  <body>
    <div id="content" class="ui-admin ui-widget">
      <h1 id="header" class="ui-widget-header ui-corner-all">
        <div class="breadcrumb">
          % for url, text, _ in breadcrumb:
            <a href="${ url|h }">${ text|h }</a>
            % if not loop.last:
            <span>/</span>
            % endif
          % endfor
        </div>
        <div>${ request.model_name or 'root'|h }</div>
      </h1>
      ${ next.body() }
    </div>
  </body>
</html>
