<%inherit file="base.mak" />

<div class="ui-pager">${ pager }</div>
${ grid.render()|n }
<p class="fa_field">
${ actions.buttons(request)|n }
</p>
