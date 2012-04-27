<%inherit file="base.mak" />

<form method="POST" enctype="multipart/form-data"
      action="">
  <div>
    ${ form.render() }
  </div>
  <input type="hidden" name="_method" value="PUT" />
  <p class="fa_field">
    ${ actions.buttons(request)|n }
  </p>
</form>

