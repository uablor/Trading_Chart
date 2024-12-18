import * as yup from 'yup';
export const userSchema = yup.object({
    name: yup.string().required('Please enter name.'),
    lastname: yup.string().required('Please enter lastname.'),
    age: yup.string().required('Please enter age.'),
});