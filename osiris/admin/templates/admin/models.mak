<%inherit file="base.mak" />

<div>
% for item in menu:
  <div>
    <a href="${ request.route_url(request.route_name, traverse=item) }">${ item }</a>
  </div>
% endfor
</div>
