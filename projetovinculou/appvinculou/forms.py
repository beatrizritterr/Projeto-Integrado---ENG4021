from django import forms

class CadastroUsuarioForm(forms.Form):
    nome_completo = forms.CharField(max_length=150, label="Nome completo:")
    nome_perfil = forms.CharField(max_length=50, label="Nome do perfil:")
    email = forms.EmailField(label="Email:")
    data_nascimento = forms.DateField(
        label="Data de nascimento:",
        widget=forms.DateInput(attrs={'type': 'date'}) 
    )
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha:")
    confirmacao_senha = forms.CharField(widget=forms.PasswordInput, label="Confirme a Senha:")

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirmacao_senha = cleaned_data.get("confirmacao_senha")

        if senha and confirmacao_senha and senha != confirmacao_senha:
            raise forms.ValidationError(
                "As senhas digitadas não são iguais. Por favor, verifique."
            )
        return cleaned_data