import { defineStore } from "pinia"
import { reactive, ref } from "vue";
import { UserService } from "../service";
import { container } from "tsyringe";
import { IForm } from "../entity";

export const UserStore = defineStore('user-store', () => {
    const service = container.resolve<UserService>(UserService);
    const state = reactive<any>({
        visible: false,
        form: reactive<IForm>({}),
        users: [
            {
                id: 1,
                name: "phet",
                lastname: "thor",
                age: 18,
                status: "active"
            },
            {
                id: 2,
                name: "admin",
                lastname: "thor",
                age: 18,
                status: "inactive"
            },
            {
                id: 3,
                name: "user",
                lastname: "thor",
                age: 18,
                status: "active"
            },
        ],
        columns: [
            {
                title: 'Name',
                dataIndex: 'name',
                key: 'name',
            },
            {
                title: 'Age',
                dataIndex: 'age',
                key: 'age',
            },
            {
                title: 'Lastname',
                dataIndex: 'lastname',
                key: 'lastname',
            },
            {
                title: 'Status',
                dataIndex: 'status',
                key: 'status',
            },
        ]
    })
    const showModal = () => {
        state.visible = true;
    };

    async function createUser() {
        await service.createUser(state.form)
    }

    return {
        state,
        showModal,
        createUser
    }
})