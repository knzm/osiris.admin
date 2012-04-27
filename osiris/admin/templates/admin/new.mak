<%inherit file="base.mak" />

<form method="POST" enctype="multipart/form-data"
      action="${ request.fa_url(request.model_name)|h }">
  <div>
    ${ form.render() }
  </div>
  <p class="fa_field">
    ${ actions.buttons(request)|n }
  </p>
</form>
