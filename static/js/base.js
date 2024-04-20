let AccountTypeForm = document.getElementById("account_type_form")


handleAccountTypeSelect = (e) => {
    
    e.currentTarget["continue"].disabled = false
}

if(AccountTypeForm)
    AccountTypeForm.addEventListener('change', handleAccountTypeSelect)