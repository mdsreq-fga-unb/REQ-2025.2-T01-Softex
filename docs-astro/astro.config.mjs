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
							label: "Contexto",
							slug: "visao/cenario",
						},
						{
							label: "Solução",
							slug: "visao/solucao",
						},
						{
							label: "Processo de Engenharia de Software",
							slug: "visao/processo-sw",
						},
						{
							label: "Comunicação e Colaboração",
							slug: "visao/interacao",
						},
						{
							label: "Cronograma",
							slug: "visao/cronograma",
						},
						{
							label: "Evidências",
							slug: "visao/evidencias",
						},
						{
							label: "Processo de Engenharia de Requisitos",
							slug: "visao/engenharia-requisitos",
						},
						{
							label: "DoR / DoD",
							slug: "visao/dor-dod",
						},
						{
							label: "Requisitos de Software",
							slug: "visao/levantamento-parcial",
						},
						{
							label: "Backlog",
							slug: "visao/backlog",
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
					{
						label: "Unidade 3",
						slug: "entregas/unidade-3",
					}
				],
			},
			],
		}),
	],
});
