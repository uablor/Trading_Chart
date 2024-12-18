<template>
    <div>
        <a-modal :open="visible" title="Basic Modal" @ok="onSubmit" @cancel="onClose">
            <a-form-item>
                <div class="whitespace-nowrap w-full">
                    User name
                </div>
                <a-input v-model:value="name" placeholder="Basic usage" />
                <span v-if="errors.name" class="text-red-600">{{ errors.name }}</span>
            </a-form-item>
            <a-form-item>
                <div class="whitespace-nowrap w-full">
                    last name
                </div>
                <a-input v-model:value="lastname" placeholder="Basic usage" :style="{ border: errors.lastname ? '2px solid red' : '2px solid black' }"/>
                <span v-if="errors.lastname" class="text-red-600">{{ errors.lastname }}</span>
            </a-form-item>
            <a-form-item>
                <div class="whitespace-nowrap w-full">
                    Age
                </div>
                <a-input v-model:value="age" placeholder="Basic usage" />
                <span v-if="errors.age" class="text-red-600">{{ errors.age }}</span>
            </a-form-item>
        </a-modal>
    </div>

</template>

<script setup lang="ts">
import { userSchema } from '../schema';
import { useForm, useField } from 'vee-validate';
import { UserStore } from '../store';
const { createUser, state } = UserStore()



defineProps({
    visible: Boolean,
})
const emits = defineEmits(["update:visible"])

const { handleSubmit, errors } = useForm({
    validationSchema: userSchema
});

const { value: name } = useField<string>('name');
const { value: lastname } = useField<string>('lastname');
const { value: age } = useField<string>('age');

const onSubmit = handleSubmit(async (value) => {
    state.form = {
        name: value.name,
        lastname: value.lastname,
        age: value.age,
    }
    // console.log('Submitted values:' + value);
    await createUser()
});

const onClose = () => {
    emits('update:visible', false)
}
</script>

<style scoped></style>