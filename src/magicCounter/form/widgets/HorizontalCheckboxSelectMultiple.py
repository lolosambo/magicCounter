from django.forms import CheckboxSelectMultiple


class HorizontalCheckboxSelectMultiple(CheckboxSelectMultiple):
    template_name = 'magicCounter/widgets/checkbox_select.html'
    option_template_name = 'magicCounter/widgets/checkbox_options.html'