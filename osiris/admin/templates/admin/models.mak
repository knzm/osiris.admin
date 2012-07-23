<%inherit file="base.mak" />

<ul>
  % for item in request.admin_menu:
    <li>
      <a href="${ request.route_url(request.route_name, traverse=item['name']) }">${ item['title'] }</a>
    </li>
  % endfor
</ul>
