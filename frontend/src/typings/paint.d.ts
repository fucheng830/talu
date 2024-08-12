declare namespace IPaintState {

    interface IState {
        listTask: IPaintState.IListTask[],
    }

    type ITaskType = 'merged' | 'zoomup'

    interface IListTask {
        type: ITaskType
        imgUrl: string
        uuid: string
    }

}