/*
 * -------------------------------
 * Difficult Rocket
 * Copyright © 2020-2023 by shenjackyuanjie 3695888@qq.com
 * All rights reserved
 * -------------------------------
 */

use pyo3::prelude::*;
use rapier2d_f64::prelude::*;

#[pyfunction]
#[pyo3(name = "simulation")]
pub fn simulation() -> () {
    let mut rigid_body_set = RigidBodySet::new();
    let mut collider_set = ColliderSet::new();

    /* Create the ground. */
    let collider = ColliderBuilder::cuboid(100.0, 0.1).build();
    let ball = ColliderBuilder::ball(10.0).build();
    collider_set.insert(collider);
    collider_set.insert(ball);

    /* Create the bouncing ball. */
    let rigid_body = RigidBodyBuilder::dynamic().translation(vector![0.0, 10.0]).build();
    let collider = ColliderBuilder::ball(0.5).restitution(0.7).build();
    let ball_body_handle = rigid_body_set.insert(rigid_body);
    collider_set.insert_with_parent(collider, ball_body_handle, &mut rigid_body_set);

    /* Create other structures necessary for the simulation. */
    let gravity = vector![0.0, -9.81];
    let integration_parameters = IntegrationParameters::default();
    let mut physics_pipeline = PhysicsPipeline::new();
    let mut island_manager = IslandManager::new();
    let mut broad_phase = BroadPhase::new();
    let mut narrow_phase = NarrowPhase::new();
    let mut impulse_joint_set = ImpulseJointSet::new();
    let mut multibody_joint_set = MultibodyJointSet::new();
    let mut ccd_solver = CCDSolver::new();
    let physics_hooks = ();
    let event_handler = ();

    /* Run the game loop, stepping the simulation once per frame. */
    for _ in 0..200 {
        physics_pipeline.step(
            &gravity,
            &integration_parameters,
            &mut island_manager,
            &mut broad_phase,
            &mut narrow_phase,
            &mut rigid_body_set,
            &mut collider_set,
            &mut impulse_joint_set,
            &mut multibody_joint_set,
            &mut ccd_solver,
            None,
            &physics_hooks,
            &event_handler,
        );

        let ball_body = &rigid_body_set[ball_body_handle];
        println!("Ball altitude: {} {}", ball_body.translation().x, ball_body.translation().y);
    }
}

pub mod interface {
    use rapier2d_f64::prelude::*;

    pub struct PhysicsSpace {
        pub rigid_body_set: RigidBodySet,
        pub collider_set: ColliderSet,
        pub gravity: Vector<f64>,
        pub integration_parameters: IntegrationParameters,
        pub physics_pipeline: PhysicsPipeline,
        pub island_manager: IslandManager,
        pub broad_phase: BroadPhase,
        pub narrow_phase: NarrowPhase,
        pub impulse_joint_set: ImpulseJointSet,
        pub multibody_joint_set: MultibodyJointSet,
        pub ccd_solver: CCDSolver,
        pub physics_hooks: (),
        pub event_handler: (),
    }

    impl PhysicsSpace {
        pub fn new(gravity: (f64, f64)) -> Self {
            let rigid_body_set = RigidBodySet::new();
            let collider_set = ColliderSet::new();
            let gravity = vector![gravity.0, gravity.1];
            let integration_parameters = IntegrationParameters::default();
            let physics_pipeline = PhysicsPipeline::new();
            let island_manager = IslandManager::new();
            let broad_phase = BroadPhase::new();
            let narrow_phase = NarrowPhase::new();
            let impulse_joint_set = ImpulseJointSet::new();
            let multibody_joint_set = MultibodyJointSet::new();
            let ccd_solver = CCDSolver::new();
            let physics_hooks = ();
            let event_handler = ();
            Self {
                rigid_body_set,
                collider_set,
                gravity,
                integration_parameters,
                physics_pipeline,
                island_manager,
                broad_phase,
                narrow_phase,
                impulse_joint_set,
                multibody_joint_set,
                ccd_solver,
                physics_hooks,
                event_handler,
            }
        }

        pub fn tick_space(&mut self) {
            self.physics_pipeline.step(
                &self.gravity,
                &self.integration_parameters,
                &mut self.island_manager,
                &mut self.broad_phase,
                &mut self.narrow_phase,
                &mut self.rigid_body_set,
                &mut self.collider_set,
                &mut self.impulse_joint_set,
                &mut self.multibody_joint_set,
                &mut self.ccd_solver,
                None,
                &self.physics_hooks,
                &self.event_handler,
            );
        }

        
    }
}
