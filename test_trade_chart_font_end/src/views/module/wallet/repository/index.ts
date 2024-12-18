import { inject, injectable } from "tsyringe";
import { IUserRepository } from "../interface";
// import { AxiosApi } from "src/common/config/axios.config";
import { AxiosApi } from "../../../../common/config/axios.config";

@injectable()
export class UserRepository implements IUserRepository {
    constructor(@inject(AxiosApi) private _api: AxiosApi) {}

    async createUser(form: any): Promise<any> {
        try {
            const response = await this._api.axios.get("room-types/");
            return response.data;
        } catch (error) {
            console.error("Error creating user:", error);
            throw error;
        }
    }
}
