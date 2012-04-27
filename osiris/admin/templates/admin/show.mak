<%inherit file="base.mak" />

<div>
<table>
${ form.render() }
</table>
</div>
<div>
<p class="fa_field">
${ actions.buttons(request)|n }
</p>
</div>

