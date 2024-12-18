import { injectable, inject } from "tsyringe";
import { UserRepository } from "../repository";
import type { IUserRepository } from '../interface/index';

@injectable()
export class UserService {
    constructor(@inject(UserRepository) private _repo: IUserRepository) { }
    async createUser(form: any): Promise<any> {
        return this._repo.createUser(form)
    }
}