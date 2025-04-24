/**
 * Interface for the calculated impact values grouped by lifecycle stages
 */

export type LifeCycleGroups = keyof ICalculatedImpact

export interface ICalculatedImpact {
    Production: number;
    Construction: number;
    Operation: number;
    Disassembly : number;
    Disposal: number;
    Reuse: number;
}