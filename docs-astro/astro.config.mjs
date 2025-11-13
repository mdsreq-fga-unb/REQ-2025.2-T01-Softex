// @ts-check

import starlight from "@astrojs/starlight";
import { defineConfig } from "astro/config";
import starlightThemeRapidePlugin from "starlight-theme-rapide";

export default defineConfig({
	site: "https://mdsreq-fga-unb.github.io",
	base: "/REQ-2025.2-T01-Softex",
	integrations: [
		starlight({
			plugins: [starlightThemeRapidePlugin()],
			title: "Softex - Sistema de Gestão de Recursos",
			head: [
				{
					tag: "link",
					attrs: {
						rel: "stylesheet",
						href: "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css",
						integrity: "sha512-2SwdPD6INVrV/lHTZbO2nodKhrnDdJK9/kg2XD1r9uGqPo1cUbujc+IYdlYdEErWNu69gVcYgdxlmVmzTWnetw==",
						crossorigin: "anonymous",
						referrerpolicy: "no-referrer"
					}
				}
			],
			social: [
				{
					icon: "github",
					label: "GitHub",
					href: "https://github.com/mdsreq-fga-unb/REQ-2025.2-T01-Softex",
				},
			],
			customCss: ['./src/styles/custom.css'],
			sidebar: [
				{
					label: "Início",
					items: [
						{
							label: "Sobre o Projeto",
							slug: "home/sobre",
						},
						{
							label: "Equipe",
							slug: "home/equipe",
						},
					],
				},
				{
					label: "Visões de Produto e de Projeto",
					items: [
						{
							label: "Contexto e Necessidades",
							slug: "visao/cenario",
						},
						{
							label: "Solução Proposta",
							slug: "visao/solucao",
						},
					
						{
							label: "Requisitos do Sistema",
							slug: "visao/levantamento-parcial",
						},
						{
							label: "Cronograma e Entregas",
							slug: "visao/cronograma",
						},
						{
							label: "Comunicação e Colaboração",
							slug: "visao/interacao",
						},
						{
							label: "Backlog do Produto",
							slug: "visao/backlog",
						},
						{
							label: "Engenharia de Requisitos",
							slug: "visao/engenharia-requisitos",
						},
					{
						label: "DoR & DoD",
						slug: "visao/dor-dod",
					},
					],
				},
			{
				label: "Lições Aprendidas",
				items: [
					{
						label: "Unidade 1",
						slug: "licoes/unidade-1",
					},
					{
						label: "Unidade 2",
						slug: "licoes/unidade-2",
					},
				],
			},
		
			{
				label: "Entregas",
				items: [
					{
						label: "Unidade 1",
						slug: "entregas/unidade-1",
					},
					{
						label: "Unidade 2",
						slug: "entregas/unidade-2",
					},
				],
			},
			],
		}),
	],
});
